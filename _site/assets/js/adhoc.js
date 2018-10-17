(function() {
    if (typeof console !== "undefined" && typeof console.log === "function") {
        var adhocGreen = "#31B77B";
        var logo = [
            "++++++   +++",
            "++++++   +++",
            "+++         ",
            "+++         ",
            "++++++   +++",
            "++++++   +++",
            "++++++++++++",
            "++++++++++++"
        ];
        console.log("%c%s\n", "font-weight: 700; color: " + adhocGreen, logo.join("\n"));
        console.log("%cAd Hoc", "font-weight: 700; font-size: 18px; color: " + adhocGreen);
        console.log("%cWe want to work with you.%c https://homework.adhoc.team/",
                    "background-color: papayawhip; color: " + adhocGreen,
                    "color: cornflowerblue");
    }

}());
