import { Avatar, Menu, Layout } from "antd";
import { UserOutlined, ShopOutlined, ShoppingCartOutlined, AppstoreOutlined, ShoppingOutlined } from '@ant-design/icons';
import { useContext } from "react";
import AuthContext from "../../contexts/AuthContext";
import { Outlet, useNavigate } from "react-router-dom";

function getItem(label, key, icon, children) {
    return {
        key,
        icon,
        label,
        children
    };
}

const items = [
    getItem("Menu", "menu", <AppstoreOutlined />, [
        getItem("Products", "products", <ShopOutlined />),
        getItem("Cart", "cart", <ShoppingCartOutlined />),
        getItem("Orders", "orders", <ShoppingOutlined />)
    ]),
]

const siderStyle = {
    backgroundColor: "red",
    justifyContent: "center",
}
const contentStyle = {
    padding: 20
}

const { Content, Sider } = Layout;
function Profile() {
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    const navigateTo = ({key}) => {
        navigate(`/profile/${key}`)
    }

    return (
        <Layout>
            <Layout>
                <Sider
                    style={siderStyle}
                    width="25%">
                    <Avatar icon={<UserOutlined />} size={100} />
                    <p>{user.username}</p>
                    <Menu
                        onClick={navigateTo}
                        items={items}
                        mode="inline"
                    />
                </Sider>
                <Content style={contentStyle}>
                    <Outlet />
                </Content>
            </Layout>
        </Layout>
    )
}

export default Profile