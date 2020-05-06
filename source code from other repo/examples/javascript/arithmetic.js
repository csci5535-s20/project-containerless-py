let containerless = require("../dist/index");

containerless.listen(function(req) {
	let foo = 2;
	let bar = foo + 3;
	let res = foo * bar;
	containerless.respond(res);
});
