
//Cargar los plugins requeridos
var gulp = require('gulp'),
	concat = require('gulp-concat'),
	jshint = require('gulp-jshint'),
	uglify = require('gulp-uglify'),
	notify = require('gulp-notify'),
	livereload = require('gulp-livereload'),
	imagemin = require('gulp-imagemin'),
	webserver = require('gulp-webserver'),
	connect = require('gulp-connect'),
	nodemon = require('gulp-nodemon'),
	exec = require('child_process').exec;


//Cargar las imágenes
gulp.task('images', function() {
	return gulp.src('static/img/*')
	.pipe(imagemin({ optimizationLevel: 5, progressive: true, interlaced: true }))
	.pipe(gulp.dest('static/img'))
	.pipe(connect.reload())
	.pipe(notify({ message: 'Images task complete' }));
});

//Cargar los archivos html
gulp.task('html', function() {
    return gulp.src('static/html/*.html')
        .pipe(gulp.dest('static/html'))
        .pipe(connect.reload())
        .pipe(notify({ message: 'HTML task complete' }))
});

//Compila los archivos js en uno solo
gulp.task('scripts', function() {
	return gulp.src('static/js/source/*.js')
	.pipe(jshint())
	.pipe(jshint.reporter('default'))
	.pipe(concat('main.js'))
	.pipe(uglify())
	.pipe(gulp.dest('static/js/build'))
	.pipe(connect.reload())
	.pipe(notify({ message: 'Scripts task complete' }));
});

//Inicia el servidor de gulp
gulp.task('webserver', function () {
  nodemon({
  	script: 'server.js'
  	, env: {'NODE': 'development'}
  })
});

// gulp.task('default', ['clean'], function() {
gulp.task('default', ['html', 'scripts', 'images', 'webserver']);

