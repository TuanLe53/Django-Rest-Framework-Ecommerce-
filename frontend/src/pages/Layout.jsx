import { useContext } from "react";
import { Outlet, Link } from "react-router-dom";
import AuthContext from "../contexts/AuthContext";
import { Divider, Flex, Layout } from "antd";

const { Header, Content, Footer } = Layout;

function PageLayout() {
    const { isLogin, handleLogout, user } = useContext(AuthContext);

    return (
        <Layout>
            <Header>
                <Flex
                    className="header"
                    justify="space-between"
                >
                    <Link to="/">Ecommerce</Link>
                    {isLogin ?
                        <Flex
                            justify="space-between"
                        >
                            <Link to="/profile">{user.username}</Link>
                            <Divider type="vertical" />
                            <p onClick={handleLogout}>Logout</p>
                        </Flex>
                        :
                        <Flex
                            justify="space-between"
                        >
                            <Link to="/login">Login</Link>
                            <Divider type="vertical" />
                            <Link to="/register">Register</Link>
                        </Flex>    
                    }
                </Flex>
            </Header>
            <Content id="main-content">
                <Outlet />
            </Content>
            <Footer>
                <p>About us</p>
            </Footer>
        </Layout>
    )
}
export default PageLayout