var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var cssmin = require('gulp-cssmin');
var rename = require('gulp-rename');

gulp.task('styles', function () {
  return gulp.src('./less/main.less')
    .pipe(less({
      paths: [ path.join(__dirname, 'less') ]
    }).on('error', function (err) {
      console.log(err);
    }))
    .pipe(gulp.dest('./css/'));
});

gulp.task('watch', function () {
  gulp.watch('./less/*.less', ['styles']);
});

gulp.task('less', function () {
  return gulp.src('./less/main.less')
    .pipe(less({
      paths: [ path.join(__dirname, 'less') ]
    }).on('error', function (err) {
      console.log(err);
    }))
    .pipe(cssmin().on('error', function(err) {
      console.log(err);
    }))
    .pipe(rename({suffix: '.min'}))
    .pipe(gulp.dest('./css/'));
});

gulp.task('default', ['less', 'watch']);
