## utx

---

> 支持Python3.5及以上版本，请留意~~

utx是对Python unittest的功能进行了扩展，起因是希望可以控制测试用例的执行顺序，unittest的默认执行顺序是按照用例函数的名称进行排序，无法满足需求。所以想要做一个可以无缝接入unittest的扩展功能库。

目前有以下的功能：

- 支持用例排序，只需要导入utx库，用例的执行顺序就会和编写顺序一致

- 支持用例自定义标签，在 case_tag.py 里边添加标签，可以对测试用例指定多标签

```python
@unique
class Tag(Enum):
    SMOKE = 1  # 冒烟测试标记，可以重命名，但是不要删除
    FULL = 1000  # 完整测试标记，可以重命名，但是不要删除

    # 以下开始为扩展标签，自行调整
    SP = 2
```

```python
class TestLegion(unittest.TestCase):

    @tag(Tag.SMOKE)
    def test_create_legion(self):
        pass
```

- 运行指定标签的测试用例

```python
from utx import *

if __name__ == '__main__':
    setting.run_case = {Tag.SMOKE}  # 只运行SMOKE冒烟用例
    # setting.run_case = {Tag.FULL}  # 运行全部测试用例
    # setting.run_case = {Tag.SMOKE, Tag.SP}   # 只运行标记为SMOKE和SP的用例

    runner = TestRunner()
    runner.run_test(r"testcase")
```

- 支持数据驱动
```python
class TestLegion(unittest.TestCase):

    @data(["gold", 100], ["diamond", 500])
    def test_bless(self, bless_type, award):
        print(bless_type)
        print(award)
        
    @data(10001, 10002, 10003)
    def test_receive_bless_box(self, box_id):
        """ 领取祈福宝箱

        :return:
        """
        print(box_id)
```

- 检测用例是否编写了用例描述
```python
2017-11-03 12:00:19,334 WARNING legion.test_legion.test_bless没有用例描述
```

- 执行测试时，显示测试进度
```python
2017-11-03 12:00:19,336 INFO 开始进行测试
2017-11-03 12:00:19,436 INFO Start to test legion.test_legion.test_create_legion (1/5)
2017-11-03 12:00:19,536 INFO Start to test legion.test_legion.test_receive_bless_box (2/5)
2017-11-03 12:00:19,637 INFO Start to test legion.test_legion.test_receive_bless_box (3/5)
2017-11-03 12:00:19,737 INFO Start to test legion.test_legion.test_receive_bless_box (4/5)
2017-11-03 12:00:19,837 INFO Start to test legion.test_legion.test_quit_legion (5/5)
```

- 集成 [ztest](https://github.com/zhangfei19841004/ztest) 和 [BSTestRunner](https://github.com/easonhan007/HTMLTestRunner) 自动生成两份测试报告，感谢两位作者的测试报告模版~

> ztest风格

![ztest风格](https://github.com/jianbing/utx/raw/master/img/ztest.png)

> BSTest风格

![BSTest风格](https://github.com/jianbing/utx/raw/master/img/bstest.png)

- 无缝接入unittest项目，导入utx包即可开始使用扩展功能，无需修改之前的代码

---

demo目录下，有两个例子：

- run.py，体验utx的完整功能~

- just_use_report.py 单独使用测试报告组件，不需要utx的其他扩展功能

