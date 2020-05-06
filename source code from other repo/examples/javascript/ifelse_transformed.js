var containerless00 = require('../dist/index');

let cb = containerless00.cb;
let exp = containerless00.exp;
cb.trace.newTrace();
let $test = exp.boolean(false);
cb.trace.traceLet("fun0", exp.clos({}));

function fun0(req) {
  let [$clos, $req] = cb.trace.traceFunctionBody("'ret");
  cb.trace.traceLet("req", $req);
  cb.trace.traceLet("return_value00", exp.number(1));
  var return_value00 = 1;
  $test = exp.binop("===", exp.number(24), exp.number(42));

  if (24 === 42) {
    cb.trace.traceIfTrue($test);
    cb.trace.traceSet(exp.identifier("return_value00"), exp.number(0));
    return_value00 = 0;
  } else {
    cb.trace.traceIfFalse($test);
    cb.trace.traceSet(exp.identifier("return_value00"), exp.number(2));
    return_value00 = 2;
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
