let containerless = require('../dist/index');

containerless.listen(function(req) {
    let return_value = 1;
    if(24 === 42) {
	return_value = 0;
    } else {
	return_value = 2;
    }
    containerless.respond(return_value);
});
