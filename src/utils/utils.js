const { exec } = require("child_process");
const { DefaultDeserializer } = require("v8");


// cmd = "cd python;"+"source doc-detect-env/bin/activate;"+"python3 src/main.py;"+"deactivate;";



async function sh(cmd) {
  return new Promise(function (resolve, reject) {
    exec(cmd, (err, stdout, stderr) => {
      if (err) {
        reject(err);
      } else {
        resolve({ stdout, stderr });
      }
    });
  });
}

async function call(cmd) {
    console.log("command executed:"+cmd);
    let { stdout } = await sh(cmd);
//   for (let line of stdout.split('\n')) {
//     console.log(`ls: ${line}`);
//   }
    console.log(stdout)
    return stdout;

  


}

module.exports= call