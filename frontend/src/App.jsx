import {BrowserRouter, Routes, Route} from "react-router-dom";
import PageLayout from "./pages/Layout";
import Home from "./pages/home/Home";
import Login from "./pages/auths/Login";
import Register from "./pages/auths/Register";
import { AuthProvider } from "./contexts/AuthContext";
import "./App.css"
import Profile from "./pages/profile/Profile";
import PrivateRoute from "./utils/PrivateRoute";
import Products from "./pages/profile/Products";
import Cart from "./pages/profile/Cart";
import Orders from "./pages/profile/Orders";
import Payment from "./pages/profile/Payment";
import ProductDetail from "./pages/product/ProductDetail";
import Order from "./pages/order/Order";

function App() {

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<PageLayout />}>
            <Route index element={<Home />} />
            <Route path="/product/:id" element={<ProductDetail />} />
            <Route path="/profile" element={<PrivateRoute component={Profile} />}>
              <Route path="products" element={<Products />} />
              <Route path="cart" element={<Cart />} />
              <Route path="orders" element={<Orders />} />
              <Route path="payment" element={<Payment />} />
            </Route>
            <Route path="create-order/" element={<Order />} />
          
          </Route>

          <Route>
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
          </Route>

        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
