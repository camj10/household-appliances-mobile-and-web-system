import React, { useState } from 'react';
import { View, Text, Button, StyleSheet, Alert, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import Modal from 'react-native-modal';

const OrderScreen = ({ route, navigation }) => {
  const { product } = route.params;
  console.log("product: ", product);
  console.log("product.id: ", product.id);
  const [error, setError] = useState('');
  const [isModalVisible, setIsModalVisible] = useState(false);

  const showSuccessModal = () => {
    setIsModalVisible(true);
  };

  const handlePlaceOrder = async () => {
    try {
      // Obtener el CSRF token
      const csrfResponse = await axios.get('http://localhost:8000/csrf-token/');
      const csrfToken = csrfResponse.data.csrfToken;
      console.log("Obtenido CSRF token: ", csrfToken);

      if (!csrfToken) {
        throw new Error('CSRF token is missing.');
      }

      // Obtener el token de acceso desde AsyncStorage
      const token = await AsyncStorage.getItem('access_token');
      const usuario = await AsyncStorage.getItem('id');
      console.log("token de authConfig: ", token);

      // Verificar que el token de acceso está presente
      if (!token) {
        throw new Error('Access token is missing.');
      }

      // Realizar la solicitud para crear el pedido
      console.log("antes de la soli product.id: ",product.id);
      const response = await axios.post('http://localhost:8000/crearpedido/', {
        producto: product.id,
        cantidad_cuotas: product.cantidad_cuotas,
        precio_cuota: product.precio_cuota,
        usuario_cliente: usuario, // Reemplazar por el usuario
      }, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        withCredentials: true // Asegúrate de que esta opción esté habilitada si estás usando cookies
      });

      if (response.status === 201) {
        showSuccessModal();
      }
    } catch (error) {
      console.error('Error placing order:', error.response ? error.response.data : error.message);
      setError('Error placing order');
    }
  };

  return (
    <View style={styles.outerContainer}>
      <View style={styles.innerContainer}>
        <Text style={styles.title}>Confirmar Pedido</Text>
        <Image source={{ uri: `http://localhost:8000/media/imagenes/${product.imagen}` }} style={styles.image} />
        <Text>Producto: {product.descripcion}</Text>
        <Text>Marca: {product.marca}</Text>
        <Text>Precio Total: {product.precio_total}</Text>
        <Text>Stock: {product.stock}</Text>
        <Text>Cantidad de Cuotas: {product.cantidad_cuotas}</Text>
        <Text>Precio por Cuota: {product.precio_cuota}</Text>
        {error ? <Text style={styles.error}>{error}</Text> : null}
        <Button title="Realizar pedido" onPress={handlePlaceOrder} />
        <Button title="Cancelar" onPress={() => navigation.goBack()} />
        <Modal
          isVisible={isModalVisible}
          onBackdropPress={() => setIsModalVisible(false)}
          style={styles.modal}
        >
          <View style={styles.modalContent}>
            <Text style={styles.modalText}>Pedido solicitado con éxito</Text>
            <Button title="OK" onPress={() => {
              setIsModalVisible(false);
              navigation.navigate('HomeScreen');
            }} />
          </View>
        </Modal>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  
  outerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f8f8f8', // Cambia el color de fondo según sea necesario
  },
  innerContainer: {
    width: '90%', // Puedes ajustar esto según sea necesario
    backgroundColor: 'white',
    padding: 20,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.8,
    shadowRadius: 2,
    elevation: 5,
  },
  container: {
    flex: 1,
    padding: 20,
  },
  image: {
    width: '100%',
    height: 200,
    resizeMode: 'contain',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginVertical: 10,
    textAlign: 'center',
  },
  error: {
    color: 'red',
  },
  modal: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalContent: {
    width: 300, // Ajusta el ancho del modal
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalText: {
    fontSize: 16,
    marginBottom: 20,
  },
});

export default OrderScreen;