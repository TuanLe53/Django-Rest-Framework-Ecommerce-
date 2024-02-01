import { Form, Input, Button } from "antd";
import URL from "../../api/urls";
import { useNavigate } from "react-router-dom";

function Register() {
    
    const navigate = useNavigate()

    const handleRegister = async (form) => {
        let res = await fetch(URL.Auth + "register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                "email": form.email,
                "password": form.password
            })
        })
        let data = await res.json()
        if (res.status === 201) {
            alert("User created")
            navigate("/login")
        } else {
            alert("Something went wrong!")
        }
    }

    return (
        <Form
            name="register"
            onSubmit={e=> e.preventDefault()}
            onFinish={handleRegister}
        >
            <Form.Item
                name="email"
                label="E-mail"
                rules={[
                {
                    type: 'email',
                    message: 'The input is not valid E-mail!',
                },
                {
                    required: true,
                    message: 'Please input your E-mail!',
                },
                ]}
            >
                <Input />
            </Form.Item>

            <Form.Item
                name="password"
                label="Password"
                rules={[
                {
                    required: true,
                    message: 'Please input your password!',
                },
                ]}
                hasFeedback
            >
                <Input.Password />
            </Form.Item>

            <Form.Item
                name="confirm"
                label="Confirm Password"
                dependencies={['password']}
                hasFeedback
                rules={[
                {
                    required: true,
                    message: 'Please confirm your password!',
                },
                ({ getFieldValue }) => ({
                    validator(_, value) {
                    if (!value || getFieldValue('password') === value) {
                        return Promise.resolve();
                    }
                    return Promise.reject(new Error('The new password that you entered do not match!'));
                    },
                }),
                ]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item>
                <Button type="primary" htmlType="submit">
                    Register
                </Button>
            </Form.Item>
        </Form>
    )
}

export default Register