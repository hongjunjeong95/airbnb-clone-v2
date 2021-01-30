import gulp from "gulp";
import postCSS from "gulp-postcss";
import sass from "gulp-sass";
import csso from "gulp-csso";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";

const path = {
  scss: {
    src: "assets/scss/styles.scss",
    dest: "static/css",
    watch: "assets/scss/**/*.scss",
  },
};

export const css = () => {
  sass.compiler = require("node-sass");
  return gulp
    .src(path.scss.src)
    .pipe(sass().on("error", sass.logError))
    .pipe(postCSS([tailwindcss, autoprefixer]))
    .pipe(csso())
    .pipe(gulp.dest(path.scss.dest));
};

const watch = () => {
  gulp.watch(path.scss.watch, css);
};

export const dev = gulp.series([css, watch]);
