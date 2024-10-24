const { BrowserWindow, getCurrentWindow, dialog } = require("@electron/remote");
const fs = require("fs");
const path = require("path");

let mainWindow = getCurrentWindow();

// 点击事件
window.addEventListener("DOMContentLoaded", () => {
  // 菜单栏操作
  const option_minimize = document.getElementById("option-minimize");
  option_minimize.addEventListener("click", () => {
    mainWindow.minimize();
  });

  const option_maximize = document.getElementById("option-maximize");
  option_maximize.addEventListener("click", () => {
    if (!mainWindow.isMaximized()) {
      mainWindow.maximize();
    } else {
      mainWindow.restore();
    }
  });

  const option_close = document.getElementById("option-close");
  option_close.addEventListener("click", () => {
    console.log("option-close");
    mainWindow.close();
  });



  var childProcess=[];
  // 监视提交表单事件
  const configButton = document.querySelector("#config");
  configButton.addEventListener("submit", function (event) {
    event.preventDefault(); // stop the form from submitting
    // 表明正在运行

    // 启动子进程
    let host = document.getElementById("config-host").value;
    if (host == "") {
      host = "127.0.0.1";
    }
    let port = document.getElementById("config-port").value;
    if (port == "") {
      port = "4398";
    }
    var protocol = document.querySelector(
      'input[name="options"]:checked'
    ).value;
    if (protocol == "") {
      protocol = "kelapa";
    }
    //require("child_process").spawn("C:\\Program Files\\010 Editor.exe");
    var python = require("child_process").spawn(
      "python",
      [
        path.join(__dirname, "/../../protocol/progServer.py"),
        "--ip=" + host,
        "--port=" + port,
        "--protocol=" + protocol,
      ],
      { stdio: "pipe" }
    );
    // 记录子进程
    childProcess.push(python);
    python.stdout.on("data", function (data) {
      // INSERT P

      var contentPart = document.createElement("p");
      contentPart.innerText = data.toString("utf8");
      contentPart.className = "log-font";
      let display_window = document.getElementById("display-box");
      display_window.innerHTML = "";
      display_window.appendChild(contentPart);
    });

    python.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    // insert status box
    let status = document.getElementById("qr-box").children[0];
    status.innerHTML = "RUNNING"+"<br>"+protocol;
    
    //
    python.on("close", (code) => {
      console.log(`child process exited with code ${code}`);
      status.innerHTML = "STOP";

    });
  });
  // 监视reset事件
  configButton.addEventListener("reset", function (event) {
    event.preventDefault();
    for(i in childProcess){
      childProcess[i].kill();
    }
    let display_window = document.getElementById("display-box");
    display_window.innerHTML = "";

    // 修改运行状态提示
    let status = document.getElementById("qr-box").children[0];
    status.innerHTML = "RUNNING"+"<br>"+protocol;
  });
});
