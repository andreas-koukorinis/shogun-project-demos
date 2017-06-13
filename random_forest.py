from modshogun import CSVFile, RealFeatures, MulticlassLabels, RandomForest, MajorityVote, CARTree, PT_MULTICLASS, MulticlassAccuracy
from numpy import array

def load_file(feat_file, label_file):
    feats = RealFeatures(CSVFile(feat_file))
    labels = MulticlassLabels(CSVFile(label_file))
    return (feats, labels)


def setup_random_forest(num_trees,rand_subset_size,combination_rule,feature_types):
    rf=RandomForest(rand_subset_size,num_trees)
    rf.set_combination_rule(combination_rule)
    rf.set_feature_types(feature_types)

    return rf

train_data_file = 'train.data'
train_label_file = 'train.label'
train_feats, train_labels = load_file(train_data_file, train_label_file)

comb_rule=MajorityVote()
feat_types=array([False]*52)
rand_forest=setup_random_forest(10, 4,comb_rule,feat_types)

rand_forest.set_labels(train_labels)
rand_forest.train(train_feats)

test_data_file ='test.data'
test_label_file = 'test.label'
test_feats,test_labels=load_file(test_data_file,test_label_file)

# apply forest
output_rand_forest_train=rand_forest.apply_multiclass(train_feats)
output_rand_forest_test=rand_forest.apply_multiclass(test_feats)

def train_cart(train_feats,train_labels,feature_types,problem_type):
    c=CARTree(feature_types,problem_type,2,False)
    c.set_labels(train_labels)
    c.train(train_feats)

    return c

# train CART
cart=train_cart(train_feats,train_labels,feat_types,PT_MULTICLASS)

# apply CART model
output_cart_train=cart.apply_multiclass(train_feats)
output_cart_test=cart.apply_multiclass(test_feats)

accuracy=MulticlassAccuracy()

rf_train_accuracy=accuracy.evaluate(output_rand_forest_train,train_labels)*100
rf_test_accuracy=accuracy.evaluate(output_rand_forest_test,test_labels)*100

cart_train_accuracy=accuracy.evaluate(output_cart_train,train_labels)*100
cart_test_accuracy=accuracy.evaluate(output_cart_test,test_labels)*100

print('Random Forest training accuracy : '+str(round(rf_train_accuracy,3))+'%')
print('CART training accuracy : '+str(round(cart_train_accuracy,3))+'%')
print
print('Random Forest test accuracy : '+str(round(rf_test_accuracy,3))+'%')
print('CART test accuracy : '+str(round(cart_test_accuracy,3))+'%')