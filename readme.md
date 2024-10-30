# 基于 PaddleOCR 的文本验证码识别

本项目提供一个基于 PaddleOCR 的验证码识别 API，支持静态图像和 GIF 动态图片。API 能识别验证码图像中的文本并返回识别结果。

## 示例图片
![code.gif](test/code.gif)

来源：https://pass.hust.edu.cn/cas/code

## 特性

* **PaddleOCR 识别**：利用 PaddleOCR 进行高效的文本识别。
* **GIF 支持**：通过合并 GIF 的所有帧生成静态图像，以提高识别准确性。
* **REST API**：提供基于 HTTP POST 的验证码识别接口。

## 环境要求

* Python 3.8 或更高版本

安装依赖：

```bash
pip install -r requirements.txt
```

## 运行应用

启动 Flask 服务器：

```bash
python main.py
```

默认地址为 `http://127.0.0.1:5000`。

## API 文档

### 接口：`/v1/image/ocr`

* **方法**：`POST`
* **Content-Type**：`application/x-www-form-urlencoded`
* **参数**：
    * `url`（可选）：验证码图片的 URL。
    * `image_base64`（可选）：Base64 编码的验证码图像。
    * `useragent`（可选）：自定义的 User-Agent，用于 URL 请求。
* **响应**：
    * **成功** (200)：返回识别的文本内容。
    * **错误** (400)：当 `url` 和 `image_base64` 均缺失时返回错误信息。

示例 cURL 请求：

```bash
curl -X POST 'http://127.0.0.1:5000/v1/image/ocr' \
-H 'Content-Type: application/x-www-form-urlencoded' \
--data-urlencode 'image_base64=R0lGODlhWgA6APcAAAAAAAEBAQICAg...'
```

`/v1/image/combined_gif`

* **方法**：`POST`
* **Content-Type**：`application/x-www-form-urlencoded`
* **参数**：
    * `url`（可选）：验证码图片的 URL。
    * `image_base64`（可选）：Base64 编码的验证码图像。
    * `useragent`（可选）：自定义的 User-Agent，用于 URL 请求。
* **响应**：
    * **成功** (200)：返回合并GIF后的静态图像内容。
    * **错误** (400)：当 `url` 和 `image_base64` 均缺失时返回错误信息。

## 基准测试

使用 Apache Benchmark (AB) 进行测试：

```bash
ab -n 1000 -c 10 -p post_data.txt -T 'application/x-www-form-urlencoded' http://127.0.0.1:5000/ocr
```

### 基准测试结果示例（纯CPU）：

```shell
CPU	Intel(R) Core(TM) i7-10870H CPU @ 2.20GHz

Server Software:        Werkzeug/3.0.6
Server Hostname:        172.16.0.209
Server Port:            5000

Document Path:          /ocr
Document Length:        4 bytes

Concurrency Level:      5
Time taken for tests:   13.862 seconds
Complete requests:      100
Failed requests:        3
   (Connect: 0, Receive: 0, Length: 3, Exceptions: 0)
Non-2xx responses:      3
Total transferred:      18546 bytes
Total body sent:        801400
HTML transferred:       1183 bytes
Requests per second:    7.21 [#/sec] (mean)
Time per request:       693.102 [ms] (mean)
Time per request:       138.620 [ms] (mean, across all concurrent requests)
Transfer rate:          1.31 [Kbytes/sec] received
                        56.46 kb/s sent
                        57.76 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   0.1      1       1
Processing:   432  667  70.9    669     897
Waiting:      407  618  70.4    625     819
Total:        433  668  70.9    670     898

Percentage of the requests served within a certain time (ms)
  50%    670
  66%    690
  75%    709
  80%    724
  90%    748
  95%    771
  98%    898
  99%    898
 100%    898 (longest request)
```
### 基准测试结果示例（GPU）：
```shell
GPU NVIDIA GeForce RTX 3060 Laptop GPU
	专用 GPU 内存	0.8/6.0 GB

Server Software:        Werkzeug/3.0.6
Server Hostname:        172.16.0.209
Server Port:            5000

Document Path:          /ocr
Document Length:        4 bytes

Concurrency Level:      10
Time taken for tests:   39.977 seconds
Complete requests:      1000
Failed requests:        18
   (Connect: 0, Receive: 0, Length: 18, Exceptions: 0)
Non-2xx responses:      18
Total transferred:      182076 bytes
Total body sent:        8014000
HTML transferred:       8698 bytes
Requests per second:    25.01 [#/sec] (mean)
Time per request:       399.769 [ms] (mean)
Time per request:       39.977 [ms] (mean, across all concurrent requests)
Transfer rate:          4.45 [Kbytes/sec] received
                        195.77 kb/s sent
                        200.22 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   10  97.7      0    1061
Processing:    85  388  54.3    385     645
Waiting:       61  357  52.7    355     615
Total:         86  398 110.8    385    1469

Percentage of the requests served within a certain time (ms)
  50%    385
  66%    410
  75%    426
  80%    435
  90%    456
  95%    488
  98%    534
  99%    645
 100%   1469 (longest request)
```

