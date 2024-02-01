import { Navigate } from 'react-router-dom';
import { useContext } from 'react';
import AuthContext from '../contexts/AuthContext';

const PrivateRoute = ({ component: Component }) => {
    let { isLogin } = useContext(AuthContext);
    return isLogin ? <Component /> : <Navigate to="/login" />;
}

export default PrivateRoute;