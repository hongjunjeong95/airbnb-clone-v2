import gulp from "gulp";
import postCSS from "gulp-postcss";
import sass from "gulp-sass";
import csso from "gulp-csso";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";
import babelify from "babelify";
import bro from "gulp-bro";
import del from "del";

const path = {
  scss: {
    src: "assets/scss/styles.scss",
    dest: "static/css",
    watch: "assets/scss/**/*.scss",
  },
  js: {
    src: "assets/js/main.js",
    dest: "static/js",
    watch: "assets/js/**/*.js",
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

const js = () =>
  gulp
    .src(path.js.src)
    .pipe(
      bro({
        transform: [babelify.configure({ presets: ["@babel/preset-env"] })],
      })
    )
    .pipe(gulp.dest(path.js.dest));

const watch = () => {
  gulp.watch(path.scss.watch, css);
  gulp.watch(path.js.watch, js);
};

const clean = () => del(["static/css/", "static/js/"]);
const assets = gulp.series([css, js]);

export const build = gulp.series([clean, assets]);
export const dev = gulp.series([build, watch]);
