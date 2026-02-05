const dns = require("dns");

process.stdout.write("Enter a URL: ");

process.stdin.once("data", (data) => {
  let url = data.toString().trim();

  url = url.replace(/^https?:\/\//, "");
  url = url.replace(/^www\./, "");
  url = url.split("/")[0];

  dns.lookup(url, (err, address) => {
    if (err) {
      console.log("Could not resolve the domain");
    } else {
      console.log(`IP Address of ${url}: ${address}`);
    }
    process.exit();
  });
});
// How to run: node Resolve-IP.js