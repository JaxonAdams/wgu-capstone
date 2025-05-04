const { spawn } = require("child_process");

function run(command, args, options = {}) {
    return spawn(command, args, { stdio: "inherit", shell: true, ...options });
}

(async () => {

    const open = (await import("open")).default;

    // Start the backend Flask server
    const server = run("python", ["-m", "src.server.app"]);

    // Wait a few seconds for the server to initialize
    await new Promise(resolve => setTimeout(resolve, 10000));

    // Start the frontend application
    const client = run("npm", ["run", "dev"], { cwd: "client" });

    // Wait a few seconds for the client to initialize
    await new Promise(resolve => setTimeout(resolve, 500));

    // Open the client in the dev's web browser
    open("http://localhost:5173");

    // Keep the script alive as long as server & client are running
    server.on("exit", code => {
        console.log(`Server exited with status code ${code}`);
        process.exit(code);
    });

    client.on("exit", code => {
        console.log(`Client exited with status code ${code}`);
        process.exit(code);
    });

})();