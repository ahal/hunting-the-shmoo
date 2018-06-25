Element.prototype.hasClass = function(name) {
    return this.className && new RegExp("(^|\\s)" + name + "(\\s|$)").test(this.className);
};

window.onload = function() {
    function isMenuActive(element) {
        return element.hasClass('active');
    }

    let nav = document.getElementsByTagName('nav')[0];
    let navlinks = Array.prototype.slice.call(nav.getElementsByTagName('a'));
    if (!navlinks.some(isMenuActive)) {
        navlinks[0].className += ' active';
    }
}
