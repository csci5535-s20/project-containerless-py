var containerless00 = require("../dist/index");

let cb = containerless00.cb;
let exp = containerless00.exp;
cb.trace.newTrace();
let $test = exp.boolean(false);
cb.trace.traceLet("fun0", exp.clos({}));

function fun0(req) {
  let [$clos, $req] = cb.trace.traceFunctionBody("'ret");
  cb.trace.traceLet("req", $req);
  cb.trace.traceLet("foo00", exp.number(2));
  var foo00 = 2;
  cb.trace.traceLet("bar00", exp.binop("+", exp.identifier("foo00"), exp.number(3)));
  var bar00 = foo00 + 3;
  cb.trace.traceLet("res00", exp.binop("*", exp.identifier("foo00"), exp.identifier("bar00")));
  var res00 = foo00 * bar00;
  cb.trace.traceFunctionCall("app1", [exp.from(exp.identifier("containerless00"), "respond"), exp.identifier("res00")]);
  let app1 = containerless00.respond(res00);
  cb.trace.exitBlock();
  cb.trace.exitBlock();
}

cb.trace.traceFunctionCall("app0", [exp.from(exp.identifier("containerless00"), "listen"), exp.identifier("fun0")]);
let app0 = containerless00.listen(fun0);
cb.trace.exitBlock();
cb.trace.exitBlock();
