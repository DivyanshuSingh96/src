/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    mode: "jit",
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        // "./templates/**/*.html",
        // "./theme/templates/**/*.html",
        // "./theme/static_src/src/**/*.css",
        // "./theme/static_src/src/**/*.js",

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {
            "width": {
                "81": "22rem",
                "82": "24rem",
                "83": "26rem",
                "84": "28rem",
                "85": "30rem",
                "86": "32rem",
                "88": "34rem",
                "90": "36rem",
                "92": "38rem",
                "94": "40rem",
                "96": "48rem",
                "97": "52rem",
            },

            "height": {
                "53": "15rem",
                "54": "17rem",
                "55": "19rem",
                "56": "21rem",
                "57": "23rem",
                "58": "25rem",
                "59": "27rem",
                "60": "29rem",
                "61": "31rem",
                "62": "33rem",
                "63": "34rem",
                "64": "35rem",
                "65": "36rem",
                "96": "48rem"
            },

            "dropShadow": {
                "3xl": "0 35px 35px rgba(78, 84, 200, 1)"
            },

            "spacing": {
                "28": "8.3rem",
                "29": "9rem",
                "30": "11rem",
                "31": "13rem"
            },

            "textColor": {
                "orangeX": "#f7971e",
                "greenX": "#34e89e",
                "blueX": "#4568dc",
                "blackX": "#6a6a6a",
            },

            textSize: {
                "3xl": "3.2rem",
            },

            "backgroundColor": {
                "orangeX": "#f7971e",
                "greenX": "#34e89e",
                "blueX": "#4568dc",
                "blackX": "#6a6a6a",
            },

            "fontFamily": {
                "poppins": "Poppins",
                "syne": "Syne Mono",
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
