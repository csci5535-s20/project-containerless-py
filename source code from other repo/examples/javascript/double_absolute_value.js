let containerless = require('../dist/index');

containerless.listen(function(req) {
    let return_value = req.body.num;
    let double_x = 2 * return_value;
    if(return_value < 0) {
	return_value = -double_x;
    } else {
	return_value = double_x;
    }
    containerless.respond(return_value);
});
