   import tensorflow as tf
   model = tf.keras.models.load_model('model.h5')
   # X_test, y_test = ... # data test Anda
   loss, acc = model.evaluate(X_test, y_test)
   print(f"Akurasi model: {acc*100:.2f}%")