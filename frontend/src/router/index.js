import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue'),
                    meta: { requiresAuth: true } // Requires authentication
                },
                {
                    path: 'user',
                    name: 'user',
                    component: () => import('@/views/User.vue')
                },
                {
                    path: 'product',
                    name: 'product',
                    component: () => import('@/views/Product.vue')
                },
                {
                    path: 'order',
                    name: 'order',
                    component: () => import('@/views/Order.vue')
                },
                {
                    path: 'report',
                    name: 'report',
                    component: () => import('@/views/Report.vue')
                },
                {
                    path: 'wallet',
                    name: 'wallet',
                    component: () => import('@/views/Wallet.vue')
                },
                {
                    path: 'notification',
                    name: 'notification',
                    component: () => import('@/views/Notification.vue')
                },
                {
                    path: 'setting',
                    name: 'setting',
                    component: () => import('@/views/Setting.vue')
                }
            ]
        },
        {
            path: '/auth',
            children: [
                {
                    path: 'login',
                    name: 'login',
                    component: () => import('@/views/pages/auth/Login.vue')
                },
                {
                    path: 'error',
                    name: 'error',
                    component: () => import('@/views/pages/auth/Error.vue')
                },
                {
                    path: 'access',
                    name: 'access',
                    component: () => import('@/views/pages/auth/Access.vue')
                }
            ]
        },
        // {
        //     path: '/usermanagement',
        //     component: AppLayout,
        //     children: [
        //         {
        //             path: '',
        //             name: 'usermanagement',
        //             component: () => import('@/views/pages/UserManagement/UserManagement.vue'),
        //             props: route => ({ tab: route.params.tab ? Number(route.params.tab) : 0 })
        //         },
        //         {
        //             path: 'permission',
        //             name: 'permission',
        //             component: () => import('@/views/pages/UserManagement/Permission.vue')

        //         },
        //         {
        //             path: 'rolespermission',
        //             name: 'rolespermission',
        //             component: () => import('@/views/pages/UserManagement/RolesManagement.vue')
        //         },
        //         {
        //             path: 'users',
        //             name: 'users',
        //             component: () => import('@/views/pages/UserManagement/Users.vue')
        //         },
        //         {
        //             path: 'accountrequest',
        //             name: 'accountrequest',
        //             component: () => import('@/views/pages/UserManagement/AccountManagement.vue'),
        //         },
        //         {
        //             path: 'adduser',
        //             name: 'adduser',
        //             component: () => import('@/views/pages/UserManagement/AddManagement.vue')
        //         },
        //     ]
        // },
        {
            path: '/usermanagement',
            component: AppLayout,
            children: [
                {
                    path: '',
                    name: 'usermanagement',
                    component: () => import('@/views/pages/UserManagement/UserManagement.vue'),
                    props: route => ({ tab: route.params.tab ? Number(route.params.tab) : 0 })
                },
                {
                    path: 'permission',
                    name: 'permission',
                    component: () => import('@/views/pages/UserManagement/Permission.vue')

                },
                {
                    path: 'rolespermission',
                    name: 'rolespermission',
                    component: () => import('@/views/pages/UserManagement/RolesManagement.vue')
                },
                {
                    path: 'users',
                    name: 'users',
                    component: () => import('@/views/pages/UserManagement/Users.vue')
                },
                {
                    path: 'accountrequest',
                    name: 'accountrequest',
                    component: () => import('@/views/pages/UserManagement/AccountManagement.vue'),
                },
                {
                    path: 'adduser',
                    name: 'adduser',
                    component: () => import('@/views/pages/UserManagement/AddManagement.vue')
                },
            ]
        },
        {
            path: '/pages',
            children: [
                {
                    path: 'empty',
                    name: 'empty',
                    component: () => import('@/views/pages/Empty.vue')
                },
                {
                    path: 'notfound',
                    name: 'notfound',
                    component: () => import('@/views/pages/NotFound.vue')
                }
            ]
        },
        {
            path: '/products',
            component: AppLayout,
            children: [
                {
                    path: 'product',
                    name: 'product',
                    component: () => import('@/views/pages/products/Product.vue')
                },
                {
                    path: 'addproduct',
                    name: 'addproduct',
                    component: () => import('@/views/pages/products/AddProduct.vue')
                },
                {
                    path: 'stock',
                    name: 'stock',
                    component: () => import('@/views/pages/products/Stock.vue')
                },
                {
                    path: 'addstock',
                    name: 'addstock',
                    component: () => import('@/views/pages/products/AddStock.vue')
                },
                {
                    path: 'controllerlist',
                    name: 'controllerlist',
                    component: () => import('@/views/pages/products/ControllerList.vue')
                }
            ]
        }
    ]
});

// Navigation guard to check for authentication
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token'); // Check if the token exists

    if (to.meta.requiresAuth && !isAuthenticated) {
        next({ name: 'login' }); // Redirect to login if not authenticated
    } else {
        next(); // Proceed to the route
    }
});

export default router;
