# wtest
Web automation test with Python and Selenium

## 1. Prepare the environment
- Install requirements: Pytest, Selenium, webdriver-manager, coverage
```bash
python3 -m pip install -r requirements.txt
```
- Download webdriver: 
  + `https://googlechromelabs.github.io/chrome-for-testing/#stable`
  + `https://github.com/mozilla/geckodriver/releases`
- For mac m1:
  + brew install --cask xquartz
  + Start X
  + export DISPLAY=:0
  + run: xhost +

## 2. Config.ini and ENV

+ Fill with proper parameters

+ If using minio as s3 alternative for local run, requires:
  + s3_access_key
  + s3_secret_key
  + s3_endpoint_url

## 3. Test cases and Test suites
- Independent test
- Cross-section test

## 4. Run test suites
```bash
# Independent test suite
python3 -m pytest webapp/testsuites/independent/test_log_in_log_out.py -vv

# Cross-section test suite
python3 -m pytest webapp/testsuites/smoke_tests/smoke_suite_admin_flow.py -vv

# Run one test case from independent test suite
python3 -m pytest webapp/testsuites/independent/test_log_in_log_out.py::TestLogInLogOut::test_user_logs_out_successfully -vv
```
