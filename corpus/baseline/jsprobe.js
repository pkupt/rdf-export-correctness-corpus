// Baseline probe: JavaScript side.
// Subcommands:
//   emit <record>            -> write the defective output of a corpus record to stdout
//   parse <format> <file>    -> exit 0 if the file parses under <format>, else exit 1
//
// Used by run_baseline.py as the "independent parser" for Python-produced output,
// and as the "own parser" for JavaScript-produced output.
//
// Resolves `n3` from the nearest node_modules (`npm install` in the directory that
// holds package.json, i.e. corpus/). Exits 2 if it cannot, so the caller can tell
// "the probe could not run" apart from "the file did not parse".

const fs = require('fs');

let N3;
try {
  N3 = require('n3');
} catch (e) {
  process.stderr.write('jsprobe: cannot load n3 (' + String(e.message || e).split('\n')[0] +
    '). Run `npm install` in the directory that holds package.json.\n');
  process.exit(2);
}

const FORMATS = {
  'turtle': 'text/turtle',
  'ttl': 'text/turtle',
  'ntriples': 'application/n-triples',
  'nt': 'application/n-triples',
  'nquads': 'application/n-quads',
  'nq': 'application/n-quads',
  'trig': 'application/trig',
};

function emit(record) {
  switch (record) {
    // C2: IRIREF-forbidden characters written through unescaped.
    case 'n3-659': {
      const w = new N3.Writer({ format: 'application/n-triples' });
      w.addQuad(
        N3.DataFactory.quad(
          N3.DataFactory.namedNode('http://example.org/s'),
          N3.DataFactory.namedNode('http://example.org/p'),
          N3.DataFactory.namedNode('http://example.org/a b<c>')
        )
      );
      w.end((err, out) => { if (err) { process.stderr.write(String(err)); process.exit(2); } process.stdout.write(out); });
      break;
    }
    // C5: asked for N-Triples, get four terms back (the writer falls through to N-Quads).
    case 'n3-165': {
      const w = new N3.Writer({ format: 'application/n-triples' });
      w.addQuad(
        N3.DataFactory.quad(
          N3.DataFactory.namedNode('http://example.org/s'),
          N3.DataFactory.namedNode('http://example.org/p'),
          N3.DataFactory.literal('v'),
          N3.DataFactory.namedNode('http://example.org/g')
        )
      );
      w.end((err, out) => { if (err) { process.stderr.write(String(err)); process.exit(2); } process.stdout.write(out); });
      break;
    }
    // C6: blank node identity split.
    case 'n3-660': {
      const w = new N3.Writer({ format: 'text/turtle' });
      const b = N3.DataFactory.blankNode('b0');
      w.addQuad(N3.DataFactory.quad(N3.DataFactory.namedNode('http://example.org/s'), N3.DataFactory.namedNode('http://example.org/p'), b));
      w.addQuad(N3.DataFactory.quad(b, N3.DataFactory.namedNode('http://example.org/q'), N3.DataFactory.literal('v')));
      w.end((err, out) => { if (err) { process.stderr.write(String(err)); process.exit(2); } process.stdout.write(out); });
      break;
    }
    // C2: IRI written unescaped so the output is not legal Turtle.
    case 'n3-659b': {
      const w = new N3.Writer({ format: 'text/turtle' });
      w.addQuad(
        N3.DataFactory.quad(
          N3.DataFactory.namedNode('http://example.org/s'),
          N3.DataFactory.namedNode('http://example.org/p'),
          N3.DataFactory.namedNode('http://example.org/with space')
        )
      );
      w.end((err, out) => { if (err) { process.stderr.write(String(err)); process.exit(2); } process.stdout.write(out); });
      break;
    }
    default:
      process.stderr.write('unknown record: ' + record + '\n');
      process.exit(3);
  }
}

function parse(fmt, file) {
  const mediaType = FORMATS[fmt.toLowerCase()] || fmt;
  const text = fs.readFileSync(file, 'utf8');
  try {
    const parser = new N3.Parser({ format: mediaType, baseIRI: 'http://example.org/' });
    parser.parse(text);
    process.stdout.write('OK\n');
    process.exit(0);
  } catch (e) {
    process.stdout.write('ERR ' + String(e.message || e).split('\n')[0] + '\n');
    process.exit(1);
  }
}

const [cmd, a1, a2] = process.argv.slice(2);
if (cmd === 'emit') emit(a1);
else if (cmd === 'parse') parse(a1, a2);
else { process.stderr.write('usage: jsprobe.js emit <record> | parse <format> <file>\n'); process.exit(4); }
