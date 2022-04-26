console.log('If you see this message, then your custom JavaScript script has run!')

setTimeout(function () {
    document.getElementsByClassName('point')[0].style.fill = "cyan"
    document.getElementsByClassName('point')[0].style.stroke = "black"
}, 6000);
