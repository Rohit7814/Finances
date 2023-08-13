// const { spawn } = require('child_process');
// module.exports.home = async function (req, res) {
//     console.log(req.body);
//     const childPython = spawn('python3', ["./script.py",req.body.name,req.body.Amount,req.body.Time,req.body.safety,req.body.ease]);
//     childPython.stdout.on('data',function(data){
//         console.log(data.toString());        
//         res.locals.data=data;
//         res.render("contact");
//     })
//     childPython.stderr.on('data',function(data){
//         console.log(`stderr : ${data}`)
//     })
//     childPython.on('close',(code)=>{
//         console.log(`child process exited with code ${code}`)
//     })
// };
const { spawn } = require('child_process');
module.exports.home = async function (req, res) {
    console.log(req.body);

    // Determine the correct Python command based on the operating system
    const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';

    const childPython = await spawn(pythonCommand, ["./script.py", req.body.name, req.body.Amount, req.body.Time, req.body.safety, req.body.ease]);

    childPython.stdout.on('data', async function (data) {
        console.log(data.toString());
        res.locals.data = data;
        res.render("contact");
    });

    childPython.stderr.on('data', function (data) {
        console.log(`stderr : ${data}`);
    });

    childPython.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
    });
};
