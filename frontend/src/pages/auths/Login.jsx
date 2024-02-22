import { useContext } from "react";
import { Link } from "react-router-dom";
import { LockOutlined, UserOutlined } from '@ant-design/icons';
import { Form, Input, Button, Checkbox, Layout } from "antd";
import AuthContext from "../../contexts/AuthContext";
import "./auth.css"

const { Content } = Layout;

function Login() {
    const { handleLogin } = useContext(AuthContext);

    return (
        <Layout className="authentication">
            <Content className="authentication-container">
                <h1 style={{"textAlign": "center"}}>Login</h1>
                <Form
                    name="login"
                    className="login-form"
                    initialValues={{
                        remember: true,
                    }}
                    onSubmit={e=> e.preventDefault()}
                    onFinish={handleLogin}>
                    <Form.Item
                        name="email"
                        rules={[{
                            required: true,
                            message: "Please input your email"
                        }]}
                    >
                        <Input prefix={<UserOutlined className="site-form-item-icon" />} placeholder="Email" />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        rules={[
                        {
                            required: true,
                            message: 'Please input your Password!',
                        },
                        ]}
                    >
                        <Input
                            prefix={<LockOutlined className="site-form-item-icon" />}
                            type="password"
                            placeholder="Password"
                        />
                    </Form.Item>

                    <Form.Item>
                        <Form.Item name="remember" valuePropName="checked" noStyle>
                            <Checkbox>Remember me</Checkbox>
                        </Form.Item>

                        <a className="login-form-forgot" href="">Forgot password?</a>
                    </Form.Item>

                    <Form.Item style={{"float": "right"}}>
                        <Button type="primary" htmlType="submit" className="login-form-button">
                            Log in
                        </Button>
                        <span> Or <Link to="/register">Register now</Link></span>
                    </Form.Item>
                </Form>
            </Content>
        </Layout>
    )
}

export default Login