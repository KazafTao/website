from django import forms


class Bootstrap:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            # 有attrs这个属性则追加
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            # 没有attrs这个属性则添加
            else:
                field.widget.attrs = {"class": "form-control"}


class BootstrapForm(Bootstrap, forms.Form):
    """为Form表单的所有字段自动添加class=form-control"""
    pass


class BootstrapModelForm(Bootstrap, forms.ModelForm):
    """为ModelForm表单的所有字段自动添加class=form-control"""
    pass
