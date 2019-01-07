# distribution of confidence that will be used as submission
plt.hist(predicted_return, bins='auto', label='Predicted confidence')
plt.hist(r_val, bins='auto',alpha=0.8, label='True market return')
plt.title("predicted confidence")
plt.legend(loc='best')
plt.xlim(-1,1)
plt.show()


#### hist
plt.hist(confidence, bins='auto')
plt.title("predicted confidence")
plt.show()