import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, Button, Modal, ActivityIndicator, Image, Dimensions } from 'react-native';
import createAxiosInstance from '../authConfig';
import AsyncStorage from '@react-native-async-storage/async-storage';

const HomeScreen = ({ navigation }) => {
  const [modalVisible, setModalVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [products, setProducts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const instance = await createAxiosInstance();
        const response = await instance.get('/listaproductos/');
        setProducts(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching products:', error.response ? error.response.data : error.message);
        setError('Error fetching products');
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleViewDetails = (productId) => {
    navigation.navigate('ProductDetailsScreen', { productId });
  };

  const handlePlaceOrder = (product) => {
    navigation.navigate('OrderScreen', { product });
  };

  const keyExtractor = (item) => {
    if (!item.id) {
      console.error('Item does not have an id:', item);
      return item.name; // Usa un campo alternativo o lanza una excepción si no tiene 'id'
    }
    return item.id.toString();
  };

  const handleLogout = async () => {
    setLoading(true);
    try {
      await AsyncStorage.removeItem('access_token');
      await AsyncStorage.removeItem('username');
      await AsyncStorage.removeItem('id');
      setLoading(false);
      navigation.navigate('LoginScreen');
      setModalVisible(false);
    } catch (error) {
      console.error('Error logging out:', error);
      setLoading(false);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.imageContainer}>
        <Image source={{ uri: `http://localhost:8000/media/imagenes/${item.imagen}` }} style={styles.cardImage} />
      </View>
      <View style={styles.cardContent}>
        <Text style={styles.title}>{item.descripcion}</Text>
        <Text>{item.marca}</Text>
        <Text>Precio: {item.precio_total}</Text>
        <Text>Stock: {item.stock}</Text>
        <TouchableOpacity onPress={() => handleViewDetails(item.id)} style={styles.button}>
          <Text style={styles.buttonText}>Ver detalles</Text>
        </TouchableOpacity>
        <Button title="Realizar pedido" onPress={() => handlePlaceOrder(item)} />
      </View>
    </View>
  );

  const renderSeparator = () => <View style={styles.separator} />;

  return (
    <View style={styles.container}>
      <View>
      <TouchableOpacity style={styles.buttonL} onPress={() => setModalVisible(true)}>
        <Text style={styles.buttonTextL}>Cerrar sesión</Text>
      </TouchableOpacity>
      </View>
      {error ? (
        <Text style={styles.error}>{error}</Text>
      ) : (
        <FlatList
          data={products}
          keyExtractor={keyExtractor}
          renderItem={renderItem}
          numColumns={2} // 2 columnas para mostrar hasta 4 cartas por fila
          columnWrapperStyle={styles.row}
          ItemSeparatorComponent={renderSeparator} // Agrega separación entre las filas
        />
      )}
      <Modal
        animationType="slide"
        transparent={true}
        visible={modalVisible}
        onRequestClose={() => setModalVisible(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <Text style={styles.modalTitle}>Cierre de Sesión</Text>
            <Text>¿Desea cerrar sesión?</Text>
            <View style={styles.buttonContainer}>
              <Button title="Cancelar" onPress={() => setModalVisible(false)} />
              <Button title="Aceptar" onPress={handleLogout} />
            </View>
            {loading && <ActivityIndicator size="large" color="#0000ff" />}
          </View>
        </View>
      </Modal>
    </View>
  );
};

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    backgroundColor: "white",
    flex: 1,
    padding: 20,
  },
  card: {
    backgroundColor: 'white',
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 5,
    marginBottom: 20, // Espacio entre las tarjetas
    width: (width / 2) - 30, // Ajusta el ancho de la carta para que se acomode en 2 columnas
    alignItems: 'center', // Centra el contenido de la carta
    overflow: 'hidden',
  },
  imageContainer: {
    width: '100%',
    height: 120, // Ajusta la altura del contenedor de la imagen
    backgroundColor: '#FF7F50', // Color de fondo para el contenedor de la imagen
    justifyContent: 'center',
    alignItems: 'center',
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  cardImage: {
    width: '100%',
    height: '100%',
    resizeMode: 'contain', 
  },
  cardContent: {
    padding: 10,
  },
  title: {
    fontSize: 16,
    fontWeight: 'bold',
  },
  button: {
    marginTop: 10,
    padding: 10,
    backgroundColor: '#EC7063',
    borderRadius: 5,
  },
  buttonL: {
    backgroundColor: 'white', 
    paddingVertical: 10, 
    paddingHorizontal: 20, 
    borderRadius: 5, 
    alignItems: 'center', 
  },
  buttonTextL: {
    color: 'red',
    textAlign: 'center',
  },
  buttonText: {
    color: 'white',
    textAlign: 'center',
  },
  error: {
    color: 'red',
  },
  modalOverlay: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)', 
  },
  modalContent: {
    width: '20%', 
    padding: 20,
    backgroundColor: 'white',
    borderRadius: 10,
    alignItems: 'center',
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    marginTop: 20,
  },
  row: {
    justifyContent: 'space-between', 
  },
  separator: {
    height: 20,
    width: '100%',
  },
});

export default HomeScreen;

