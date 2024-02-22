import { Form, Input, Button, Layout } from "antd";
import URL from "../../api/urls";
import { useNavigate } from "react-router-dom";
import "./auth.css"

const { Content } = Layout;

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
        <Layout className="authentication">
            <Content className="authentication-container">
                <h1 style={{"textAlign": "center"}}>Register</h1>
                <Form
                    name="register"
                    onSubmit={e=> e.preventDefault()}
                    onFinish={handleRegister}
                >
                    <Form.Item
                        name="email"
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
                        <Input placeholder="Email"/>
                    </Form.Item>

                    <Form.Item
                        name="password"
                        rules={[
                        {
                            required: true,
                            message: 'Please input your password!',
                        },
                        ]}
                        hasFeedback
                    >
                        <Input.Password placeholder="Password"/>
                    </Form.Item>

                    <Form.Item
                        name="confirm"
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
                        <Input.Password placeholder="Confirm password"/>
                    </Form.Item>

                    <Form.Item
                        style={{
                            "display": "flex",
                            "justifyContent": "center"
                        }}
                    >
                        <Button type="primary" htmlType="submit">
                            Register
                        </Button>
                    </Form.Item>
                </Form>
            </Content>
        </Layout>
    )
}

export default Register