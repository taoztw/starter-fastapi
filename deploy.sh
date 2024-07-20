ACTION=$1


# 创建pid目录
if [ ! -d "pids" ]; then
  mkdir pids
fi

# 创建 logs目录
if [ ! -d "logs" ]; then
  mkdir logs
fi


app_start() {
  nohup python main.py >server.log 2>&1 & echo $! > pids/main.pid && echo "主进程已启动"
  nohup celery -A exts.celery_exts worker --pool=solo -l info  > logs/celery.log 2>&1 & echo $! > pids/celery.pid && echo "celery 已启动"

}

app_stop() {
  echo "停止服务中..."
  kill -9 `cat pids/celery.pid`
  lsof -i  tcp:5571 | awk '{if ($2!="PID") print $2}' | xargs kill -9
  echo "停止服务完成"
}



app_restart() {
  app_stop
  app_start

}

case "$ACTION" in
  stop)
    app_stop
  ;;
  start)
    app_start
  ;;
  restart)
    app_restart
  ;;
  *)
    usage
  ;;
esac