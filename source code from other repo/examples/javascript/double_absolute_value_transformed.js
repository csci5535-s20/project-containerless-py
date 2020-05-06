var containerless00 = require('../dist/index');

let cb = containerless00.cb;
let exp = containerless00.exp;
cb.trace.newTrace();
let $test = exp.boolean(false);
cb.trace.traceLet("fun0", exp.clos({}));

function fun0(req) {
  let [$clos, $req] = cb.trace.traceFunctionBody("'ret");
  cb.trace.traceLet("req", $req);
  cb.trace.traceLet("return_value00", exp.get(exp.get(exp.identifier("req"), "body"), "num"));
  var return_value00 = req.body.num;
  cb.trace.traceLet("double_x00", exp.binop("*", exp.number(2), exp.identifier("return_value00")));
  var double_x00 = 2 * return_value00;
  $test = exp.binop("<", exp.identifier("return_value00"), exp.number(0));

  if (return_value00 < 0) {
    cb.trace.traceIfTrue($test);
    cb.trace.traceSet(exp.identifier("return_value00"), exp.op1("-", exp.identifier("double_x00")));
    return_value00 = -double_x00;
  } else {
    cb.trace.traceIfFalse($test);
    cb.trace.traceSet(exp.identifier("return_value00"), exp.identifier("double_x00"));
    return_value00 = double_x00;
  }

  cb.trace.exitBlock();
  cb.trace.traceFunctionCall("app1", [exp.from(exp.identifier("containerless00"), "respond"), exp.identifier("return_value00")]);
  let app1 = containerless00.respond(return_value00);
  cb.trace.exitBlock();
  cb.trace.exitBlock();
}

cb.trace.traceFunctionCall("app0", [exp.from(exp.identifier("containerless00"), "listen"), exp.identifier("fun0")]);
let app0 = containerless00.listen(fun0);
cb.trace.exitBlock();
cb.trace.exitBlock();
