---
title: "How to Work on Taskcluster Github"
date: 2022-10-31T16:45:00-04:00
tags: [taskcluster, github, mozilla]
slug: taskcluster-github-dev
---

[Taskcluster Github][0] is the [Taskcluster][1] service responsible for kick starting tasks on
Github repositories. At a high level:

1. You install a [Taskcluster app from the Github marketplace][2].
2. This app sends webhooks to the Github service.
3. Upon receiving a webhook, the Github service processes your repository's [.taskcluster.yml][3]
   file.
4. The Github service schedules tasks (if any) and updates the Github checks suite, or comments on
   your push / pull-request if there is an error.

While the service itself is relatively simple, testing it locally can be a pain! One approach might
be to try and synthesize Github's webhook events, and then intercept the network requests that the
Github service makes in response. But this is tricky to do, and without actually *seeing* the
results in a proper Github repo, it's hard to be sure that your changes are working as intended.

Ideally you would have a real repo, with a development version of the app listed in the Github
Marketplace, hooked up to a Taskcluster Github service running on your local machine. This way you could
trigger webhooks by performing real actions in your repo (such as opening a pull-request). Better
yet, you could see exactly how your Github service changes react!

Thanks to a lot of great work from Yarik, this is easier than ever and is all documented (or linked
to) from [this page][4]. If you are already familiar with Taskcluster development, or enjoy figuring
things out yourself, you may wish to skip this post and read the docs instead. But if you are a
Taskcluster newbie, and would appreciate some hand holding, follow along for a step by step tutorial
on how to work on and test Taskcluster Github!

[0]: https://docs.taskcluster.net/docs/reference/integrations/github
[1]: https://taskcluster.net/
[2]: https://github.com/apps/firefoxci-taskcluster
[3]: https://docs.taskcluster.net/docs/reference/integrations/github/taskcluster-yml-v1
[4]: https://github.com/taskcluster/taskcluster/blob/main/dev-docs/development-process.md#running-everything-locally-using-docker-compose

<!--more-->

# Running Taskcluster Github Locally

Before going too far down the rabbit hole, let's make sure you can run Taskcluster Github
locally in the first place.

## Pre-requisites

If you don't have the [Taskcluster monorepo][5] cloned already, start by cloning it:

```bash
git clone https://github.com/taskcluster/taskcluster
cd taskcluster
```

You'll need a specific version of `node` to run various operations in the repo. It's recommended to
use [nvm][7.5] to facilitate this. Follow the installation instructions, then run:

```bash
nvm install
nvm use
```

This will automatically install the correct version defined in `.nvmrc`. You'll also want `yarn`:

```bash
npm install -g yarn
```

Services can be run with Docker. So if you don't already, make sure both [docker][6] and the [docker
compose][7] plugin are installed and working properly.

[5]: https://github.com/taskcluster/taskcluster
[6]: https://docs.docker.com/get-docker/
[7]: https://docs.docker.com/compose/install/
[7.5]: https://github.com/nvm-sh/nvm

## Edit `hosts` File

All Taskcluster web services are served via nginx through a single `taskcluster` proxy reachable
through [http://taskcluster](http://taskcluster) on the localhost. To solve some authentication issues, it's necessary to
add the following to your hosts file:

```bash
127.0.0.1 taskcluster
```

On Linux and Mac, the hosts file is located at `/etc/hosts`. On Windows it can be found under
`C:\Windows\System32\drivers\etc\hosts`.

## Start the Services

Now you're ready to start the web services:

```bash
yarn start
```

Note that `yarn start` and `yarn stop` are [simple wrappers][8] around `docker compose`. If you are
comfortable with `docker compose` and want more control, feel free to use it directly.

Now navigate to [http://taskcluster](http://taskcluster) and verify that a Taskcluster instance is running.

[8]: https://github.com/taskcluster/taskcluster/blob/c403ef448e04819b9f04f997434f2c20d570a07c/package.json#L189

## Start the Github Service

By default, `yarn start` does not run any of the background services so we'll have to start our
Github service explicitly:

```bash
yarn start github-background-worker
```

To verify it is running simply check the logs and make sure there is output with no obvious errors:

```bash
docker compose logs github-background-worker
```


# Connecting your Service to Github

Now that you're confident you can run the Github service locally, we need to somehow connect it to
Github.

## Expose the Service to the Internet

First let's just get the service accessible to the internet. To accomplish this, we'll use a tool
called [ngrok][9]. Follow these steps to get it running:

1. First [download and install][10] ngrok.
2. Next [sign up for a free account][11].
3. Then run the command `ngrok config add-authtoken <token>`. Your token can be found in your
   dashboard after logging in.
4. Finally, run `ngrok http --host-header=taskcluster taskcluster:80`.

To test that it's working, visit [http://127.0.0.1:4040/][14], click through to the custom URL displayed
on the main page (you may need to accept a warning first) and verify that it takes you to your
Taskcluster instance's homepage.

[9]: https://ngrok.com/
[10]: https://ngrok.com/download
[11]: https://dashboard.ngrok.com/signup

## Create a Github App

Now that we can access our Taskcluster instance from the web, let's create a Github App that sends
webhooks to it. You can follow along the [Taskcluster documentation here][12]. But the gist is to:

1. Follow Github's [guide for creating a new app][13] (prefer a personal app over an organization app).
2. Select a name for your app (e.g `<name>-dev-taskcluster`).
3. Paste the `ngrok` URL from earlier into the Homepage field. This URL should look something like
   `https://<unique-id>.ngrok.com`.
4. Under webhook URL paste `https://<unique-id>.ngrok.com/api/github/v1/github`.
5. Create an arbitrary value for the secret and save it for later.
6. Set the permissions according to the [Taskcluster deployment guide][12].
7. Save the app. Github should prompt you to generate a new private key, do so and save the `.pem`
   file Github sends you for later.

[12]: https://docs.taskcluster.net/docs/manual/deploying/github
[13]: https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app

## Install the App into a Test Repo

Before we configure the Github service, let's make sure our app is working as expected:

1. Create a new empty repository (with a README) that will be used to test your Github service.
2. Navigate to the public page for your newly created Github app. This should be of the form
   `https://github.com/apps/<name>-dev-taskcluster`, but is also linked to from the app
   settings page.
3. Click `Configure`.
4. Under `Repository access` select the repo you created in step 1, then click `Save`. The app
   should now be installed in your repository. You can go to your repository settings, then click
   `Github apps` near the bottom left. Verify you see your app listed.
5. Now in one tab, open your [local ngrok dashboard][14]. In another perform some
   repository actions (e.g edit the README using the Github interface, then do a push or pull
   request).
6. Hop back over to your `ngrok` tab and verify it is receiving webhook events. The responses will
   all be "502 Bad Gateway" because we haven't configured the Github service for your app yet. But
   this is fine, for now we've verified that the webhook events from your test repo are being
   forwarded to your local machine.

[14]: http://127.0.0.1:4040/

## Configure the App in your Taskcluster instance

For the last piece, we need to configure your local Taskcluster Github service to accept webhook
events from your application. This is [also documented in the Taskcluster dev-docs][15], but to
summarize:

1. Create a new [override file][16] called `docker-compose.override.yml` at the root of the
   Taskcluster repository. This will allow you to overwrite certain docker configuration items
   without needing to commit them into the repo.
2. Add the following as the contents:
```yaml
services:
  github-web:
    environment: &ref1
      - GITHUB_PRIVATE_PEM="-----BEGIN RSA PRIVATE KEY-----\n<private key>\n-----END RSA PRIVATE KEY-----\n"
      - GITHUB_APP_ID=<app id>
      - WEBHOOK_SECRET=<secret>
      - LEVEL=debug
      - DEBUG=*
  github-background-worker:
    environment: *ref1
```
3. Replace `<private key>` with the contents of the `.pem` file (between `BEGIN RSA PRIVATE KEY` and
   `END RSA PRIVATE KEY`) you downloaded from Github.
4. Replace `<app id>` with the id of your Github app. This can be found in the "About" section on
   your app settings page.
5. Replace `<secret>` with the secret you saved for later when creating the app.

[15]: https://github.com/taskcluster/taskcluster/blob/main/dev-docs/development-process.md#start-github-services-in-development-mode
[16]: https://docs.docker.com/compose/extends

# Testing your Github Service

Et voila! You should now have a Github app connected to a Taskcluster Github service
running on your local machine. Let's make sure everything is working!

## Restart the Services

To pick up the new configuration in the override file, restart the services:

```bash
docker stop taskcluster-github-background-worker-1
docker-compose down
yarn start
yarn start github-background-worker
```

## Generate Events in Github

Now go back to your test repository and generate some more pushes or pull requests. Check your
[ngrok dashboard][17]. This time, you should see a proper response from the server! Typically either
`201` for events that Taskcluster Github knows how to handle, or `204` otherwise.

[17]: http://127.0.0.1:4040/

## Create Some "Real" Tasks

While your server is now responding to webhooks as expected, your test repository still isn't
configured to run any actual tasks. Configuring and setting up worker pools is out of scope for this
tutorial, but luckily the `docker-compose` environment comes with a pool you can use out of the
box!

1. Create a file called `.taskcluster.yml` at the root of your test repository.
2. Add the following contents:
```yaml
version: 1
reporting: checks-v1
policy:
  pullRequests: public
tasks:
  - taskQueueId: docker-compose/generic-worker
    schedulerId: taskcluster-ui
    created: {$fromNow: ''}
    deadline: {$fromNow: '1 day'}
    payload:
      command:
        - - /bin/bash
          - '-c'
          - echo "Hello World!"; exit 1
      maxRunTime: 30
    metadata:
      name: example-task
      description: An **example** task
      owner: user@example.com
      source: http://taskcluster/tasks/create
```
3. Now go and create some more pushes or pull requests. This time you should see your Taskcluster
   Github service adding a comment about missing scopes!

## Create the Missing Scopes

1. First navigate to the web UI of your instance at [http://taskcluster](http://taskcluster)
2. Click Sign In at the top right
3. Use `static/taskcluster/root` as the Client ID, the Access Token can be found in the [docker
   compose env][18] for the `auth-web` service. Search for `static/taskcluster/root` then copy the
   associated `accessToken` into the login page.
4. Leave `json-certificate` blank and login.
5. Open the side bar (top left), then select "Authorization" -> "Roles".
6. Use the plus button (bottom right) to create a new role.
7. For the "Role ID" use `repo:github.com/<user>/<repo>:*`. Replace `<user>` and `<repo>` to point
   at your test repository.
8. Under "Scopes" add the following:
```bash
queue:create-task:highest:docker-compose/generic-worker
queue:create-task:project:none
queue:scheduler-id:taskcluster-ui
```
9. Save the role.
10. Finally go and generate some more events in your repository. This time, Taskcluster Github should
   schedule an actual task which prints "Hello World"!

## Run the Github Service in Development mode

While testing, you may notice that changes to your local Taskcluster Github service aren't reflected
automatically in your deployment. Luckily this is easily remedied by starting the Github service in
development mode:
```bash
docker stop taskcluster-github-background-worker-1
yarn dev:start github-background-worker
```

Now you'll no longer need to restart the service to pick up changes! Try it out by tailing the log,
adding some print statements and re-generating an event in Github. You should see your print
statements in the console output!

## Replaying Webhook Events

Manually creating pull requests or pushes to trigger webhook events on every single code iteration
can be tedious! Luckily ngrok has a replay feature that will let you replay an incoming request.
This way, you only need to generate the event in Github once, then simply press the `Replay` button
in your ngrok dashboard to send it again! Just beware that the Github service may only take certain
actions once (e.g, if a comment about missing scopes already exists, it won't add a second one). In
those cases, you may need to re-create a fresh pull-request / push to reproduce the behaviour you
want.

# Conclusion

Whew, that was quite a journey. But once everything is in place, it makes iterating on Taskcluster
Github *so* much faster, while also giving you confidence that your changes are doing what you
expect, before hitting production!

Happy developing and good luck!


[18]: https://github.com/taskcluster/taskcluster/blob/main/docker/env/.auth

