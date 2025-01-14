$(document).ready(function () {
    const $sideMenu = $('#sideMenu');
    const $overlay = $('#overlay');
    const $sideMenuBtn = $('#sideMenuBtn');
    const $closeMenuBtn = $('#closeMenuBtn');
    const openMenu = () => {
      $sideMenu.css('left', '0');
      $overlay.show();
    };
    const closeMenu = () => {
      $sideMenu.css('left', '-300px');
      $overlay.hide();
    };
    $sideMenuBtn.on('click', openMenu);
    $closeMenuBtn.on('click', closeMenu);
    $overlay.on('click', closeMenu);
});