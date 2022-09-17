/*

青龙变量
需要刷的次数：ylgy_needTimes
需要的token：ylgy_token

================Loon==============
[Script]
cron "/10 * * * *" hw_ylgy.js, tag:羊了个羊
cron "/10 * * * *" script-path=https://raw.githubusercontent.com/yuanter/hw/main/hw_ylgy.js,tag=羊了个羊
*/
const needTimes = process.env.ylgy_needTimes
const token = process.env.ylgy_token

if(needTimes == null || needTimes == undefined){
    needTimes = 666
}

if(token == null || token == "" || token == undefined){
    token = ""
}

const axios = require("axios")
const request = axios.create({
    headers: {
        t: token
    },
    timeout: 300000,
});

function add() {
    return new Promise((resolve, reject) => {
        request.get("https://cat-match.easygame2021.com/sheep/v1/game/game_over?rank_score=1&rank_state=1&rank_time=1&rank_role=0&skin=1").then(async res => {
            if (res.data.err_code === 0 && res.data.err_msg === '') {
                let times = await getTimes();
                resolve({ msg: "成功", current:times})
            }
        }).catch(() => {
            resolve({ msg: "未知错误，进行下一次..."})
        })
    })
}

function getTimes() {
    return new Promise((resolve, reject) => {
        request("https://cat-match.easygame2021.com/sheep/v1/game/personal_info?").then(res => {
            if (res.data.err_code === 0 && res.data.err_msg === '') {
                resolve(res.data.data.daily_count)
            } else {
                resolve(-1)
            }
        }).catch(() => {
            resolve(-1)
        })
    })
}


async function start(otime) {
    let times = await getTimes();
    if (times >= 0) {
        if (times === otime) {
            console.log("当前" + times + "次，已完成。");
        } else if (times > otime) {
            console.log("当前" + times + "次，已超出，停止执行...");
        } else {
            console.log("当前" + times + "次，即将开始...");
            let _current = times
            while (otime > _current){
                let obj = await add();
                _current = obj.current;
                if(_current == undefined){
                    _current = 0
                }
                console.log(obj);
            }
            console.log("当前" + _current + "次，已完成。");
        }
    } else {
        console.log("请检查token是否正确");
        return false;
    }
}
start(needTimes)
