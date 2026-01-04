Require Import Coq.Arith.Arith.
Require Import Coq.Bool.Bool.
Require Import Coq.Logic.FunctionalExtensionality.

Section ChaincodeHLF.


Parameter ProductId RatingId : Type.
Parameter ProductId_eq_dec : forall x y : ProductId, {x = y} + {x <> y}.
Parameter RatingId_eq_dec : forall x y : RatingId, {x = y} + {x <> y}.

Record State := {
  product_exists : ProductId -> bool;
  quantity : ProductId -> nat;
  sold : ProductId -> nat;

  rating_exists : RatingId -> bool;
  rating_value : RatingId -> nat;
  rating_product : RatingId -> ProductId
}.

Definition valid_state (s : State) : Prop :=
  (forall r, rating_exists s r = true -> 1 <= rating_value s r <= 5) /\
  (forall r, rating_exists s r = true -> product_exists s (rating_product s r) = true) /\
  (forall p, sold s p > 0 -> product_exists s p = true).


Definition buy_product_q (p : ProductId) (q : nat) (s : State) : option State :=
  let current_qty := quantity s p in
  if q <=? current_qty then
    Some {|
      product_exists := product_exists s;
      quantity := fun pid => if ProductId_eq_dec pid p then current_qty - q else quantity s pid;
      sold := fun pid => if ProductId_eq_dec pid p then sold s pid + q else sold s pid;
      rating_exists := rating_exists s;
      rating_value := rating_value s;
      rating_product := rating_product s
    |}
  else None.


Definition delete_product (p : ProductId) (s : State) : State :=
  {|
    product_exists := fun pid => if ProductId_eq_dec pid p then false else product_exists s pid;
    quantity := quantity s;
    sold := sold s;
    rating_exists := fun r => if ProductId_eq_dec (rating_product s r) p then false else rating_exists s r;
    rating_value := rating_value s;
    rating_product := rating_product s
  |}.


Definition add_rating (r : RatingId) (p : ProductId) (v : nat) (s : State) : option State :=
  let ok_prod := product_exists s p in
  let ok_sold := (0 <? sold s p) in
  let ok_v := andb (1 <=? v) (v <=? 5) in
  if andb ok_prod (andb ok_sold ok_v) then
    Some {|
      product_exists := product_exists s;
      quantity := quantity s;
      sold := sold s;
      rating_exists := fun rid => if RatingId_eq_dec rid r then true else rating_exists s rid;
      rating_value := fun rid => if RatingId_eq_dec rid r then v else rating_value s rid;
      rating_product := fun rid => if RatingId_eq_dec rid r then p else rating_product s rid
    |}
  else None.


Theorem buy_delete_rate_none :
  forall s s' s'' p r v q,
    valid_state s ->
    buy_product_q p q s = Some s' ->
    s'' = delete_product p s' ->
    add_rating r p v s'' = None.
Proof.
  intros s s' s'' p r v q Hvalid Hbuy Hdelete.
  subst s''.
  unfold add_rating, delete_product, buy_product_q.
  simpl.
  destruct (ProductId_eq_dec p p) as [Heq|Hneq]; [|exfalso; apply Hneq; reflexivity].
  reflexivity.
Qed.


Check buy_delete_rate_none.


End ChaincodeHLF.
