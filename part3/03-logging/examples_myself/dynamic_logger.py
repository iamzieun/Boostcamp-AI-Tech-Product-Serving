### 1.2 dynamic logging config
import logging
import sys


dynamic_logger = logging.getLogger()
dynamic_logger.setLevel(logging.DEBUG)              # logging level이 DEBUG 이상인 메시지만 기록
log_handler = logging.StreamHandler(sys.stdout)     # 로그 메시지를 표준 출력으로 보내는 handler 생성
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")   # 로그 메시지 형식 지정
log_handler.setFormatter(formatter)
dynamic_logger.addHandler(log_handler)              # handler를 logger에 추가: 로깅된 메시지가 handler로 전달되고, handler는 지정된 형식에 맞춰 메시지를 출력

dynamic_logger.info("Hello world !")
