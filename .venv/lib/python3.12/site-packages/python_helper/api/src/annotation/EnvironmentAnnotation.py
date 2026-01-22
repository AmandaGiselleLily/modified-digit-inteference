from python_helper.api.src.service import SettingHelper, ReflectionHelper, ObjectHelper

def EnvironmentVariable(*outerArgs, environmentVariables=None, **outerKwargs) :
    def innerMethodWrapper(resourceInstanceMethod,*innerMethodArgs,**innerMethodKwargs) :
        def innerResourceInstanceMethod(*innerArgs,**innerKwargs) :
            methodReturn = None
            wraperException = None
            originalEnvironmentVariables, originalActiveEnvironment = SettingHelper.extractEnvironmentVariables(environmentVariables)
            try :
                methodReturn = resourceInstanceMethod(*innerArgs,**innerKwargs)
            except Exception as exception :
                wraperException = exception
            SettingHelper.recoverEnvironmentVariables(environmentVariables, originalEnvironmentVariables, originalActiveEnvironment)
            if ObjectHelper.isNotNone(wraperException) :
                raise wraperException
            return methodReturn
        ReflectionHelper.overrideSignatures(innerResourceInstanceMethod, resourceInstanceMethod)
        return innerResourceInstanceMethod
    return innerMethodWrapper
