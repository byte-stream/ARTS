> 随着模块的增多和复杂度不断增加，如何处理统一的返回结果成了前后端数据交互的一个重要问题，对异常进行统一处理然后返回统一的异常信息能极大地减少前后端数据交互问题。  
   
#### 如何进行全局统一异常处理？  
  
  SpringBoot提供了两个重要的注`@ControllerAdvice` 和 `@ExceptionHandle` 我们通过代码来了解一下这两个注解的使用：  
    
    @ControllerAdvice(annotations = RestController.class)
    public class RestExceptionHandler {
        private static final Logger LOGGER = LoggerFactory.getLogger(RestExceptionHandler.class);
        @ExceptionHandler
        @ResponseBody
        @ResponseStatus(HttpStatus.BAD_REQUEST)
        private <T> RestResult<T> runtimeExceptionHandler(Exception e) {
            LOGGER.error("huge error!", e);
            return RestResultGenerator.genErrorResult(ErrorCode.SERVER_ERROR);
        }
        @ExceptionHandler(MethodArgumentNotValidException.class)
        @ResponseBody
        @ResponseStatus(HttpStatus.BAD_REQUEST)
        private <T> RestResult<T> illegalParamsExceptionHandler(MethodArgumentNotValidException e) {
            LOGGER.error("invalid request!", e);
            return RestResultGenerator.genErrorResult(ErrorCode.ILLEGAL_PARAMS);
        }
    }  
      
通过代码可以大致了解到`@ControllerAdvice`在类上添加，而`@ExceptionHandle`则在方法上添加。根据自己的业务需求来完成异常的拦截处理。    
  
如果只是使用`@ExceptionHandle`只能在当前类中进行异常拦截，但是和`@ControllerAdvice`配合使用之后可以根据`@ControllerAdvice`配置的值，如示例中的`annotation = RestController.class`，就可以拦截所有被`@RestController` 注解标注的类产生的异常，并对其统一处理。  
  
#### 下面看看核心代码：  
  
  统一异常处理类`RestResult`：  
    
    public class RestResult<T> {

        private boolean result;
        private String message;
        private T data;

        private RestResult() {}
    
        public static <T> RestResult<T> newInstance() {
            return new RestResult<>();
        }

        // ...setter and getter

        @Override
        public String toString() {
            return "RestResult{" +
                    "result=" + result +
                    ", message='" + message + '\'' +
                    ", data=" + data +
                    '}';
        }
    }  
      
  被`@RestController`标注的`UserRestController` 类： 
    
    @RestController
    @RequestMapping("/api/users")
    public class UserRestController {

    @Autowired
    IUserService userService;

    /**
     * get all user, GET
     * @return
     */
    @RequestMapping(value = "", method = RequestMethod.GET)
    public RestResult<List<User>> all() {
        List<User> all = userService.findAll();
        return RestResultGenerator.genSuccessResult(all);
    }

    /**
     * add single user
     * @param user username, password
     * @return RestResult
     * @throws Exception valid check
     */
    @RequestMapping(value = "", method = RequestMethod.POST)
    public RestResult<User> save(@Valid @RequestBody User user) throws Exception {
        User save = userService.save(user);
        return RestResultGenerator.genSuccessResult(save);
    }

    /**
     * get single user by id, GET /id
     * @param id user id
     * @return RestResult<User>
     * @throws Exception
     */
    @RequestMapping(value = "/{id}", method = RequestMethod.GET)
    public RestResult<User> get(@PathVariable Long id) throws Exception {
        User user = userService.findById(id);
        return RestResultGenerator.genSuccessResult(user);
    }

    /**
     * delete user by id
     * @param id user id
     * @return success
     * @throws Exception
     */
    @RequestMapping(value = "/{id}", method = RequestMethod.DELETE)
    public RestResult delete(@PathVariable Long id) throws Exception {
        userService.delete(id);
        return RestResultGenerator.genSuccessResult();
    }

    /**
     * update user for all props
     * @param id update user id
     * @param newUser new props
     * @return updated User
     * @throws Exception
     */
    @RequestMapping(value = "/{id}", method = RequestMethod.PUT)
    public RestResult<User> updateAll(@PathVariable Long id, @Valid @RequestBody User newUser) throws Exception {
        User user = userService.findById(id);
        // copy all new user props to user except id
        BeanUtils.copyProperties(newUser, user, "id");
        user = userService.save(user);
        return RestResultGenerator.genSuccessResult(user);
    }

    /**
     * update user for some props
     * @param id update user id
     * @param newUser some props
     * @return updated user
     * @throws Exception
     */
    @RequestMapping(value = "/{id}", method = RequestMethod.PATCH)
    public RestResult<User> update(@PathVariable Long id, @Valid @RequestBody User newUser) throws Exception {
        User user = userService.findById(id);
        // copy all new user props to user except null props
        BeanUtils.copyProperties(newUser, user, Utils.getNullPropertyNames(newUser));
        user = userService.save(user);
        return RestResultGenerator.genSuccessResult(user);
    }
    }  
      
 
#### 小结：  
`@ControllerAdvice`也有局限性，只有当进入`Controller`层的时候才会被`@ControllerAdvice`处理。**拦截器抛出的错误**，以及**访问错误地址**的情况`@ControllerAdvice` 处理不了，由Spring Boot默认的**异常处理机制**处理。