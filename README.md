# utx

> 支持Python3.3以上版本，请留意~~

对Python unittest的功能进行了一些扩展

- 支持用例排序，只需要导入utx库，用例的执行顺序就会和编写顺序一致

- 支持用例自定义标签，可以运行指定标签的测试用例

```python
class TestLegion(unittest.TestCase):

    @tag(Tag.SMOKE)
    def test_create_legion(self):
        pass

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

- 用例描述检测
```python
2017-11-03 12:00:19,334 WARNING legion.test_legion.test_bless没有用例描述
```

- 测试进度展示
```python
2017-11-03 12:00:19,336 INFO 开始进行测试
2017-11-03 12:00:19,436 INFO Start to test legion.test_legion.test_create_legion (1/5)
2017-11-03 12:00:19,536 INFO Start to test legion.test_legion.test_receive_bless_box (2/5)
2017-11-03 12:00:19,637 INFO Start to test legion.test_legion.test_receive_bless_box (3/5)
2017-11-03 12:00:19,737 INFO Start to test legion.test_legion.test_receive_bless_box (4/5)
2017-11-03 12:00:19,837 INFO Start to test legion.test_legion.test_quit_legion (5/5)
```

- 集成BSTestRunner自动生成测试报告

- 无缝接入unittest项目，导入utx包即可开始使用扩展功能，无需修改之前的代码

运行demo目录下的run.py，开始体验吧~
