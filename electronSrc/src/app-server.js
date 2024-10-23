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

    python.stdout.on("data", function (data) {
      // INSERT P
      console.error(`Error: ${data.toString().trim()}`);
      //   var contentPart = document.createElement("p");
      //   contentPart.innerText = data.toString("utf8");
      //   contentPart.className = "log-font";
      //   let display_window = document.getElementById("qr-box");
      //   display_window.innerHTML = "";
      //   display_window.appendChild(contentPart);
    });

    python.stderr.on("data", (data) => {
      console.error(`stderr: ${data}`);
    });

    python.on("close", (code) => {
      console.log(`child process exited with code ${code}`);
    });
  });
  // 监视reset事件
  configButton.addEventListener("reset", function (event) {
    // event.preventDefault(); // stop the form from submitting
    // let config_form = document.getElementById("config");
    // config_form.reset();
    // let display_window = document.getElementById("display-box");
    // display_window.innerHTML = "";
    // let qr_windows = document.getElementById("qr-box");
    // qr_windows.innerHTML = "";
  });
});
