var containerless00 = require("../dist/index");

let cb = containerless00.cb;
let exp = containerless00.exp;
cb.trace.newTrace();
let $test = exp.boolean(false);
cb.trace.traceLet("fun0", exp.clos({}));

function fun0(req) {
  let [$clos, $req] = cb.trace.traceFunctionBody("'ret");
  cb.trace.traceLet("req", $req);
  cb.trace.traceFunctionCall("app1", [exp.from(exp.identifier("containerless00"), "respond"), exp.get(exp.identifier("req"), "path")]);
  let app1 = containerless00.respond(req.path);
  cb.trace.exitBlock();
  cb.trace.exitBlock();
}

cb.trace.traceFunctionCall("app0", [exp.from(exp.identifier("containerless00"), "listen"), exp.identifier("fun0")]);
let app0 = containerless00.listen(fun0);
cb.trace.exitBlock();
cb.trace.exitBlock();
