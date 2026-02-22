const dns = require("dns");
const readline = require("readline");

console.log("Node Network Monitor Running...\n");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// CTRL+C handler
process.on("SIGINT", () => {
  console.log("\nStopping monitor safely...");
  rl.close();
  process.exit(0);
});

function resolveHost(host) {
  dns.lookup(host, (err, address) => {
    if (err) {
      console.log("Error:", err.message);
      return;
    }

    console.log(`Resolved ${host} -> ${address}`);
  });
}

function ask() {
  rl.question("Enter website: ", (site) => {
    resolveHost(site);
    ask();
  });
}

ask();
