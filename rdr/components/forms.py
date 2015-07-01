# encoding: utf-8

from wtforms import Form as BaseForm


class Form(BaseForm):

    @property
    def errors_dict(self):
        result = {}
        for name, errors in self.errors.iteritems():
            if errors:
                field_err = errors[0]
                if not isinstance(field_err, dict):
                    if isinstance(field_err, basestring):
                        field_err = {
                            'reason': 'other',
                            'text': field_err
                        }
                    else:
                        raise Exception('Unknown error format on ' + name)

                result[name] = field_err

        return result

