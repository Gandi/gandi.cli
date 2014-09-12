var gulp = require('gulp');
var less = require('gulp-less');
var path = require('path');
var watch = require('gulp-watch');

gulp.task('styles', function () {
  gulp.src('./less/main.less')
    .pipe(less({
      paths: [ path.join(__dirname, 'less') ]
    }))
    .pipe(gulp.dest('./css/'));
});

gulp.task('watch', function () {
  gulp.watch('./less/*.less', ['styles']);
});
