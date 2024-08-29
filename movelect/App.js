import React, { useEffect, useState } from 'react';
import { View, Text, Modal, Button, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import NetInfo from '@react-native-community/netinfo';
import { addEventListener } from "@react-native-community/netinfo";
import AuthLoadingScreen from './src/screens/authloadingscreen';
import LoginScreen from './src/login/login';
import HomeScreen from './src/screens/homescreen';
import ProductDetailScreen from './src/screens/ProductDetailsScreen';
import OrderScreen from './src/screens/OrderScreen'; 
import AccountStatusScreen from './src/screens/AccountStatusScreen';
import OrdersScreen from './src/screens/OrderListScreen';
import Icon from 'react-native-vector-icons/FontAwesome';

const AuthStack = createStackNavigator();
const AppTabs = createBottomTabNavigator();
const AppStack = createStackNavigator();

const AuthStackNavigator = () => (
  <AuthStack.Navigator screenOptions={{ headerShown: false }}>
    <AuthStack.Screen name="LoginScreen" component={LoginScreen} />
    <AuthStack.Screen name="ProductDetailsScreen" component={ProductDetailScreen} />
    <AuthStack.Screen name="OrderScreen" component={OrderScreen} />
  </AuthStack.Navigator>
);

const AppTabsNavigator = () => (
  <AppTabs.Navigator>
    <AppTabs.Screen name="Catálogo de productos" component={HomeScreen} 
          options={{
            tabBarLabel: 'Catálogo',
            tabBarIcon: ({ color, size }) => (
              <Icon name="home" size={size} color={color} /> // Aquí configuras el ícono
            ),
          }} /> 
    <AppTabs.Screen name="Estado de cuenta" component={AccountStatusScreen}           
          options={{
            tabBarLabel: 'Estado de cuenta',
            tabBarIcon: ({ color, size }) => (
              <Icon name="dollar" size={size} color={color} /> // Aquí configuras el ícono
            ),
          }}/> 
    <AppTabs.Screen name="Mis pedidos" component={OrdersScreen} 
          options={{
            tabBarLabel: 'Mis pedidos',
            tabBarIcon: ({ color, size }) => (
              <Icon name="shopping-cart" size={size} color={color} /> // Aquí configuras el ícono
            ),
          }}/>
  </AppTabs.Navigator>
);

const App = () => {
  const [isConnected, setIsConnected] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);

  const checkServerConnection = async () => {
    try {
      const response = await fetch('http://localhost:8000/status', { method: 'GET' });
      if (response.ok) {
        setIsConnected(true);
        setModalVisible(false);
      } else {
        throw new Error('Server responded with an error');
      }
    } catch (error) {
      setIsConnected(false);
      setModalVisible(true);
    }
  };

  useEffect(() => {
    checkServerConnection(); // Verifica la conexión al iniciar
    const interval = setInterval(checkServerConnection, 60000); // Verifica la conexión cada 60 segundos

    return () => clearInterval(interval); // Limpia el intervalo cuando el componente se desmonte
  }, []);


  return (
    <>
      <Modal
        transparent={true}
        visible={modalVisible}
        animationType="slide"
      >
        <View style={styles.modalBackground}>
          <View style={styles.modalContainer}>
            <Text style={styles.modalText}>No tienes conexión en este momento. Vuelva a intentarlo más tarde</Text>
            <Button style={styles.modalButton}
              title="Cerrar"
              onPress={() => setModalVisible(false)}
            />
          </View>
        </View>
      </Modal>
      <NavigationContainer>
        <AppStack.Navigator screenOptions={{ headerShown: false }}>
          <AppStack.Screen name="AuthLoadingScreen" component={AuthLoadingScreen} />
          <AppStack.Screen name="Auth" component={AuthStackNavigator} />
          <AppStack.Screen name="AppTabs" component={AppTabsNavigator} />
          <AppStack.Screen name="ProductDetailsScreen" component={ProductDetailScreen} />
          <AppStack.Screen name="OrderScreen" component={OrderScreen} />
          <AppStack.Screen name="OrdersScreen" component={OrdersScreen} />
          <AppStack.Screen name="LoginScreen" component={LoginScreen} />
        </AppStack.Navigator>
      </NavigationContainer>
    </>
  );
};

const styles = StyleSheet.create({
  modalBackground: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  modalContainer: {
    width: 300,
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalText: {
    fontSize: 18,
    marginBottom: 10,
  },
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalButton: {
    borderColor: 'white',
    borderRadius: 10,
  }
});

export default App;
