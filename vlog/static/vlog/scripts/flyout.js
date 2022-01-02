let navlinks = document.querySelectorAll('.navlink');
var wideScreen = window.matchMedia("(min-width: 600px)");

for (let i = 0; i < navlinks.length; i++) {
    let flyoutMenu = navlinks[i].querySelector('.flyout');

    if (flyoutMenu) {

        navlinks[i].addEventListener('mouseover', function() {
            // Don't run flyout code on small-sized screens
            if (wideScreen.matches) {
                updateFlyout(navlinks[i], '5px solid darkgreen', '0px', 'visible');
            }
        });

        navlinks[i].addEventListener('mouseout', function() {
            if (wideScreen.matches) {
                updateFlyout(navlinks[i], 'none', '5px', 'hidden');
            }
        });

        // Reset nav link display if screensize is changed
        wideScreen.addListener(function() {
            if (wideScreen.matches) {
                updateFlyout(navlinks[i], 'none', '5px', 'hidden');
            } else {
                updateFlyout(navlinks[i], '5px solid darkgreen', '0px', 'hidden');
             }
        });

    }
}

function updateFlyout(navlink, linkBorder, linkPadding, flyoutVisibility) {

    let flyout = navlink.querySelector('.flyout')
    flyout.style.visibility = flyoutVisibility;

    let navlinkClasses = navlink.classList;
    for (let j = 0; j < navlinkClasses.length; j++) {
        if (navlinkClasses[j] === 'selected') {
            let link = navlink.querySelector('a')
            link.style.borderBottom = linkBorder;
            link.style.paddingBottom = linkPadding;
        }
    }

};
