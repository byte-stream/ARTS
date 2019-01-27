> 为什么使用JSON作为函数参数

由于我们在创建函数的时候，会需要传入形参，来对变量进行定义。但有时在大的工程中，我们需要传入的参数比较多，就会造成传入的形参过多，但当我们需要修改时，需要改动很多地方。所以使用JSON格式作为参数传到函数中，解决了这一问题

1. 可以随机增加或删除参数，且可以不用考虑其顺序，因为其构造十分明显

```
// 普通方法 
function commonArg(name,age,desc){
  var userinfo="name: "+name+","+"age: "+age+"\ndescription: "+desc;
    alert(userinfo);
}
commonArg("yemoo",22,"a boy!")
缺陷： 1、若参数过多时，导致括号内的长度过长
       2、只能按照参数的顺序，进行传参，否则返回的信息会不正确
       3、当不想传参时，则需要设置null值

// JSON传参方式
function JsonArg(json){
  this.name = json.name;
  this.age = json.age;
  this.desc = json.desc;
}

JsonArg.prototype.user = function(){
  console.log('name:'+this.name+'age:'+ this.age + '特征:'+(this.desc||empty));
}
var jsonArg1 = new JsonArg({name:'chen',age:20,desc:'是个男的'});
var jsonArg2 = new JsonArg({name:'chen',age:20});
jsonArg1.user();
jsonArg2.user();
```

总结：使用JSON作为参数有诸多的优点

   1.可以减少参数的传入量。只需要传一个进去即可

   2.由于JSON有key值，所以传实参时，不需要过去主义顺序

   3.每次只需要传入需要的参数即可